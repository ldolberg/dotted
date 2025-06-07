import React, { useState } from 'react';
import { Form, Input, Button, Card, Alert, Typography, Row, Col, Divider } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const { Title, Text } = Typography;

const LoginPage = () => {
  const [form] = Form.useForm();
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const { login, register, loading } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (values) => {
    setError('');
    const result = await login(values.email, values.password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
  };

  const handleRegister = async (values) => {
    setError('');
    const result = await register(values.email, values.password, values.name);
    
    if (result.success) {
      setIsRegistering(false);
      setError('');
      form.resetFields();
      // Show success message or auto-login
      alert('Registration successful! Please login with your credentials.');
    } else {
      setError(result.error);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
    form.resetFields();
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <Row justify="center" style={{ width: '100%' }}>
        <Col xs={22} sm={16} md={12} lg={8} xl={6}>
          <Card
            style={{
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              borderRadius: '8px'
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <Title level={2} style={{ color: '#1890ff', marginBottom: 8 }}>
                {isRegistering ? 'Create Account' : 'Welcome Back'}
              </Title>
              <Text type="secondary">
                {isRegistering 
                  ? 'Sign up for your SaaS Reminder account' 
                  : 'Sign in to your SaaS Reminder account'
                }
              </Text>
            </div>

            {error && (
              <Alert
                message={error}
                type="error"
                showIcon
                style={{ marginBottom: 16 }}
              />
            )}

            <Form
              form={form}
              name={isRegistering ? 'register' : 'login'}
              onFinish={isRegistering ? handleRegister : handleLogin}
              layout="vertical"
              size="large"
            >
              {isRegistering && (
                <Form.Item
                  name="name"
                  label="Full Name"
                  rules={[
                    { required: true, message: 'Please enter your full name!' },
                    { min: 2, message: 'Name must be at least 2 characters!' }
                  ]}
                >
                  <Input
                    prefix={<UserOutlined />}
                    placeholder="Enter your full name"
                  />
                </Form.Item>
              )}

              <Form.Item
                name="email"
                label="Email Address"
                rules={[
                  { required: true, message: 'Please enter your email!' },
                  { type: 'email', message: 'Please enter a valid email!' }
                ]}
              >
                <Input
                  prefix={<MailOutlined />}
                  placeholder="Enter your email"
                />
              </Form.Item>

              <Form.Item
                name="password"
                label="Password"
                rules={[
                  { required: true, message: 'Please enter your password!' },
                  { min: 6, message: 'Password must be at least 6 characters!' }
                ]}
              >
                <Input.Password
                  prefix={<LockOutlined />}
                  placeholder="Enter your password"
                />
              </Form.Item>

              {isRegistering && (
                <Form.Item
                  name="confirmPassword"
                  label="Confirm Password"
                  dependencies={['password']}
                  rules={[
                    { required: true, message: 'Please confirm your password!' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('password') === value) {
                          return Promise.resolve();
                        }
                        return Promise.reject(new Error('Passwords do not match!'));
                      },
                    }),
                  ]}
                >
                  <Input.Password
                    prefix={<LockOutlined />}
                    placeholder="Confirm your password"
                  />
                </Form.Item>
              )}

              <Form.Item style={{ marginBottom: 12 }}>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                  style={{ height: 40 }}
                >
                  {isRegistering ? 'Create Account' : 'Sign In'}
                </Button>
              </Form.Item>
            </Form>

            <Divider />

            <div style={{ textAlign: 'center' }}>
              <Text>
                {isRegistering ? 'Already have an account?' : "Don't have an account?"}
              </Text>
              <Button
                type="link"
                onClick={toggleMode}
                style={{ padding: '0 4px' }}
              >
                {isRegistering ? 'Sign In' : 'Create Account'}
              </Button>
            </div>

            {!isRegistering && (
              <div style={{ textAlign: 'center', marginTop: 12 }}>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  Demo credentials: admin@test.com / admin123
                </Text>
              </div>
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default LoginPage; 