'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import type { MenuProps } from 'antd';
import { Layout, Menu, ConfigProvider, theme, Breadcrumb } from 'antd';
import { TeamOutlined, VideoCameraOutlined } from '@ant-design/icons';
import { Inter } from 'next/font/google';

import '@/styles/global.css';
import StyledComponentsRegistry from '@/components/AntdRegistry';

const inter = Inter({ subsets: ['latin'] });
const { Header, Sider, Content } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

function getItem(
  label: React.ReactNode,
  key: React.Key,
  icon?: React.ReactNode,
  children?: MenuItem[],
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem('Swarms', 'swarms', <TeamOutlined />),
  getItem('Generations', 'generations', <VideoCameraOutlined />),
];

const RootLayout: React.FC = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const pathSnippets = pathname.split('/').filter((i) => i);
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgLayout },
  } = theme.useToken();

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
      >
        <Header style={{ padding: 0 }} />
        <Menu
          theme="dark"
          defaultSelectedKeys={['1']}
          mode="inline"
          items={items}
          onClick={({ key }) => {
            router.push(key);
          }}
        />
      </Sider>
      <Layout>
        <Content style={{ margin: '0 16px' }}>
          <Breadcrumb style={{ margin: '16px 0' }}>
            {pathSnippets.map((snippet, index) => {
              const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
              return (
                <Breadcrumb.Item key={url}>
                  <Link href={url}>{snippet}</Link>
                </Breadcrumb.Item>
              );
            })}
          </Breadcrumb>
          <Layout
            style={{
              padding: 24,
              minHeight: 360,
              background: colorBgLayout,
            }}
          >
            {children}
          </Layout>
        </Content>
      </Layout>
    </Layout>
  );
};

const Root: React.FC = ({ children }) => {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ConfigProvider
          theme={{
            algorithm: theme.darkAlgorithm,
          }}
        >
          <StyledComponentsRegistry>
            <RootLayout>{children}</RootLayout>
          </StyledComponentsRegistry>
        </ConfigProvider>
      </body>
    </html>
  );
};

export default Root;
