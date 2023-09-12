import classNames from 'classnames';
import React, { useState } from 'react';
import MyRoutes from '../components/Routes';
import Sidebar from './Sidebar';
import Footer from './Footer';

const Layout = () => {
  const [collapsed, setSidebarCollapsed] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);

  return (
    <div className='relative min-h-screen'>
      <div
        className={classNames({
          'grid bg-zinc-100': true,
          'grid-cols-sidebar': !collapsed,
          'grid-cols-sidebar-collapsed': collapsed,
          'transition-[grid-template-columns] duration-300 ease-in-out': true,
        })}
      >
        <Sidebar
          collapsed={collapsed}
          setCollapsed={setSidebarCollapsed}
          shown={showSidebar}
        />
        <div className='container mx-auto p-8'>
          <MyRoutes />
        </div>
      </div>
      {/*<Footer />*/}
    </div>
  );
};

export default Layout;
