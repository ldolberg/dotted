import React, { useEffect, useState } from 'react';
import { Table, Button, Space, message, Popconfirm } from 'antd';
import { patientApi } from '../../services/patientApi';
import AppLayout from '../../components/AppLayout';
import PatientFormModal from '../../components/PatientFormModal';
import moment from 'moment';

const PatientListPage = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);
  const [confirmLoading, setConfirmLoading] = useState(false);

  const calculateAge = (dateOfBirth) => {
    if (!dateOfBirth) return 'N/A';
    const birthDate = moment(dateOfBirth);
    if (!birthDate.isValid()) return 'Invalid Date';
    return moment().diff(birthDate, 'years');
  };

  const loadPatients = async () => {
    setLoading(true);
    try {
      const data = await patientApi.fetchPatients();
      const processedPatients = data.map(patient => ({
        ...patient,
        age: calculateAge(patient.date_of_birth),
      }));
      setPatients(processedPatients);
    } catch (error) {
      console.error('Error fetching patients:', error);
      message.error('Failed to fetch patients.');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const handleEdit = (patient) => {
    setEditingPatient(patient);
    setIsModalVisible(true);
  };

  const handleDelete = async (patientId) => {
    console.log('Delete patient:', patientId);
    try {
      await patientApi.deletePatient(patientId);
      message.success('Patient deleted successfully!');
      loadPatients();
    } catch (error) {
      console.error('Error deleting patient:', error);
      message.error('Failed to delete patient.');
    }
  };

  const handleAddNewPatient = () => {
    setEditingPatient(null);
    setIsModalVisible(true);
  };

  const handleFormSubmit = async (values) => {
    setConfirmLoading(true);
    try {
      if (editingPatient) {
        await patientApi.updatePatient(editingPatient.id, values);
        message.success('Patient updated successfully!');
      } else {
        await patientApi.createPatient(values);
        message.success('Patient added successfully!');
      }
      setIsModalVisible(false);
      setEditingPatient(null);
      loadPatients();
    } catch (error) {
      console.error('Error submitting patient form:', error);
      if (error.response && error.response.data && error.response.data.details) {
        Object.entries(error.response.data.details).forEach(([key, value]) => {
          message.error(`${key}: ${value}`);
        });
      } else {
        message.error('Failed to save patient. Check console for details.');
      }
    } finally {
      setConfirmLoading(false);
    }
  };

  const columns = [
    {
      title: 'First Name',
      dataIndex: 'first_name',
      key: 'first_name',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Last Name',
      dataIndex: 'last_name',
      key: 'last_name',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Phone Number',
      dataIndex: 'phone_number',
      key: 'phone_number',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button type="link" onClick={() => handleEdit(record)}>
            Edit
          </Button>
          <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" danger>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <AppLayout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h1>Patient List</h1>
        <Button type="primary" onClick={handleAddNewPatient}>
          New Patient
        </Button>
      </div>
      <Table
        dataSource={patients}
        columns={columns}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />

      <PatientFormModal
        visible={isModalVisible}
        initialValues={editingPatient}
        onCancel={() => {
          setIsModalVisible(false);
          setEditingPatient(null);
        }}
        onFinish={handleFormSubmit}
        confirmLoading={confirmLoading}
      />
    </AppLayout>
  );
};

export default PatientListPage;