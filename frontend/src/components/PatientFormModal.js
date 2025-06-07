import React, { useEffect } from 'react';
import { Modal, Form, Input, Button, DatePicker } from 'antd';
import moment from 'moment';

const PatientFormModal = ({ visible, onCancel, onFinish, initialValues, confirmLoading }) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (visible) {
      form.setFieldsValue({
        ...initialValues,
        date_of_birth: initialValues?.date_of_birth ? moment(initialValues.date_of_birth) : null,
      });
    } else {
      form.resetFields(); // Reset fields when modal is closed
    }
  }, [visible, initialValues, form]);

  const handleOk = () => {
    form
      .validateFields()
      .then((values) => {
        onFinish({
          ...values,
          date_of_birth: values.date_of_birth ? values.date_of_birth.format('YYYY-MM-DD') : null,
        });
      })
      .catch((info) => {
        console.log('Validate Failed:', info);
      });
  };

  return (
    <Modal
      visible={visible}
      title={initialValues ? 'Edit Patient' : 'Add New Patient'}
      okText={initialValues ? 'Update' : 'Create'}
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={handleOk}
      confirmLoading={confirmLoading}
    >
      <Form
        form={form}
        layout="vertical"
        name="patient_form"
      >
        <Form.Item
          name="first_name"
          label="First Name"
          rules={[{ required: true, message: 'Please input the first name!' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="last_name"
          label="Last Name"
          rules={[{ required: true, message: 'Please input the last name!' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="date_of_birth"
          label="Date of Birth"
          rules={[{ required: true, message: 'Please select the date of birth!' }]}
        >
          <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
        </Form.Item>
        <Form.Item
          name="email"
          label="Email"
          rules={[{ required: true, message: 'Please input the email!', type: 'email' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="phone_number"
          label="Phone Number"
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="address_street"
          label="Street Address"
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="address_city"
          label="City"
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="address_state"
          label="State"
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="address_zip"
          label="Zip Code"
        >
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default PatientFormModal; 