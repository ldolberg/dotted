import React from 'react';
import { Layout, Menu } from 'antd';
import { UserOutlined, TeamOutlined } from '@ant-design/icons';
import { Link, useLocation } from 'react-router-dom';

const { Sider, Content } = Layout;

const AppLayout = ({ children }) => {
  const location = useLocation();
  
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
        <Content style={{ margin: '24px 16px', padding: 24, minHeight: 280, background: '#fff' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout; 