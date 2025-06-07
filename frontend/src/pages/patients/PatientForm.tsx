import React, { useEffect } from 'react';
import { Form, Input, Button, DatePicker, message } from 'antd';
import dayjs from 'dayjs';
// Assume patientApi exists and has fetchPatientById, createPatient, and updatePatient methods
import patientApi from '../../api/patientApi'; // Adjust the import path as needed

interface PatientFormProps {
  patientId?: string; // Optional patientId for edit mode
  onSuccess?: () => void; // Callback after successful submission
}

const PatientForm: React.FC<PatientFormProps> = ({ patientId, onSuccess }) => {
  const [form] = Form.useForm();
  const isEditMode = !!patientId;

  useEffect(() => {
    if (isEditMode && patientId) {
      // Fetch patient data and populate the form
      patientApi.fetchPatientById(patientId)
        .then(patient => {
          form.setFieldsValue({
            ...patient,
            // Populate form fields with fetched patient data
            dateOfBirth: patient.dateOfBirth ? dayjs(patient.dateOfBirth) : null
            // For date fields, use dayjs(patient.dateField)
          });
        })
        .catch(error => {
          message.error('Failed to fetch patient data.');
          console.error('Error fetching patient:', error);
        });
    }
  }, [patientId, isEditMode, form]);

  const onFinish = (values: any) => {
    const patientData = {
      ...values,
      // Format date fields if necessary, e.g., values.dateField.toISOString()
      dateOfBirth: values.dateOfBirth ? values.dateOfBirth.toISOString() : null,
    };

    if (isEditMode && patientId) {
      // Update existing patient
      patientApi.updatePatient(patientId, patientData)
        .then(() => {
          message.success('Patient updated successfully!');
          if (onSuccess) onSuccess();
        })
        .catch(error => {
          message.error('Failed to update patient.');
          console.error('Error updating patient:', error);
        });
    } else {
      // Create new patient
      patientApi.createPatient(patientData)
        .then(() => {
          message.success('Patient created successfully!');
          form.resetFields();
          if (onSuccess) onSuccess();
        })
        .catch(error => {
          message.error('Failed to create patient.');
          console.error('Error creating patient:', error);
        });
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{
        // Default values for new patient form if any
      }}
    >
      <Form.Item
        name="name"
        label="Name"
        rules={[{ required: true, message: 'Please enter patient name!' }]}
      >
        <Input />
      </Form.Item>

      {/* Add more form fields here based on your patient schema */}
      {/* Example: Date of Birth */}
      
      <Form.Item
        name="dateOfBirth"
        label="Date of Birth"
        rules={[{ required: true, message: 'Please select date of birth!' }]}
      >
        <DatePicker format="YYYY-MM-DD" />
      </Form.Item>
      

      <Form.Item>
        <Button type="primary" htmlType="submit">
          {isEditMode ? 'Update Patient' : 'Create Patient'}
        </Button>
      </Form.Item>
    </Form>
  );
};

export default PatientForm; 