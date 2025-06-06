import React, { useEffect, useState } from 'react';
import { Table, Button } from 'antd';
import { patientApi } from '../../services/patientApi';

interface Patient {
  id: number;
  name: string;
  age: number;
  diagnosis: string;
}

const PatientListPage: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const loadPatients = async () => {
      setLoading(true);
      try {
        const data = await patientApi.fetchPatients();
        setPatients(data);
      } catch (error) {
        console.error('Error fetching patients:', error);
      }
      setLoading(false);
    };

    loadPatients();
  }, []);

  const handleEdit = (patientId: number) => {
    console.log('Edit patient:', patientId);
  };

  const handleDelete = async (patientId: number) => {
    console.log('Delete patient:', patientId);
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Diagnosis',
      dataIndex: 'diagnosis',
      key: 'diagnosis',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text: any, record: any) => (
        <span>
          <Button type="link" onClick={() => handleEdit(record.id)}>
            Edit
          </Button>
          <Button type="link" danger onClick={() => handleDelete(record.id)}>
            Delete
          </Button>
        </span>
      ),
    },
  ];

  return (
    <div>
      <h1>Patient List</h1>
      <Table
        dataSource={patients}
        columns={columns}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default PatientListPage;