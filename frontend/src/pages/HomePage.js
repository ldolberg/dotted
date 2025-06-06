import React from 'react';
import { Layout, Menu } from 'antd';
import { UserOutlined } from '@ant-design/icons';

const { Sider, Content } = Layout;

const HomePage = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <div className="demo-logo-vertical" style={{ height: 32, background: 'rgba(255, 255, 255, 0.3)', margin: 16 }} />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
          <Menu.Item key="1" icon={<UserOutlined />}>
            Users
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Content style={{ margin: '24px 16px', padding: 24, minHeight: 280, background: '#fff' }}>
          <h1>Welcome to the Homepage</h1>
          <p>This is the main dashboard area.</p>
        </Content>
      </Layout>
    </Layout>
  );
};

export default HomePage; 