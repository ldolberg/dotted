import React from 'react';
import { Layout, Menu, Button, Space, Typography } from 'antd';
import { UserOutlined, TeamOutlined, LogoutOutlined } from '@ant-design/icons';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

const AppLayout = ({ children }) => {
  const location = useLocation();
  const { user, logout } = useAuth();
  
  // Determine selected key based on current route
  const getSelectedKey = () => {
    if (location.pathname === '/patients') return ['2'];
    return ['1']; // Default to Dashboard/Home
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <div className="demo-logo-vertical" style={{ height: 32, background: 'rgba(255, 255, 255, 0.3)', margin: 16 }} />
        <Menu theme="dark" mode="inline" selectedKeys={getSelectedKey()}>
          <Menu.Item key="1" icon={<UserOutlined />}>
            <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
              Dashboard
            </Link>
          </Menu.Item>
          <Menu.Item key="2" icon={<TeamOutlined />}>
            <Link to="/patients" style={{ color: 'inherit', textDecoration: 'none' }}>
              Patients
            </Link>
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div />
          <Space>
            <Text>Welcome, {user?.name || user?.email || 'User'}</Text>
            <Button 
              type="text" 
              icon={<LogoutOutlined />} 
              onClick={logout}
            >
              Logout
            </Button>
          </Space>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, minHeight: 280, background: '#fff' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout; 