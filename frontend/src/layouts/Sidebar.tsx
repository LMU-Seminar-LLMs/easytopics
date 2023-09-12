import React, { useRef } from 'react';
import { Link } from 'react-router-dom';
import classNames from 'classnames';
import { NavItems, NavItem } from '../components/NavItems';
import {
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon,
} from '@heroicons/react/24/outline';

// add NavItem prop to component prop
type SidebarProps = {
  collapsed: boolean;
  navItems?: NavItem[];
  setCollapsed(collapsed: boolean): void;
  shown: boolean;
};

const Sidebar = ({
  collapsed,
  navItems = NavItems,
  shown,
  setCollapsed,
}: SidebarProps) => {
  const Icon = collapsed ? ChevronDoubleRightIcon : ChevronDoubleLeftIcon;
  return (
    <div
      className={classNames({
        'bg-indigo-700 text-zinc-50 fixed md:static md:translate-x-0 z-20':
          true,
        'transition-all duration-300 ease-in-out': true,
        'w-[200px]': !collapsed,
        'w-16': collapsed,
        '-translate-x-full': !shown,
      })}
    >
      <div
        className={classNames({
          'flex flex-col justify-between h-screen sticky inset-0 w-full': true,
        })}
      >
        {/* logo and collapse button */}
        <div
          className={classNames({
            'flex items-center border-b border-b-indigo-800 transition-none':
              true,
            'p-4 justify-between': !collapsed,
            'py-4 justify-center': collapsed,
          })}
        >
          {!collapsed && (
            <span className='whitespace-nowrap text-2xl'>Easytopics</span>
          )}
          <button
            className='grid place-content-center hover:bg-indigo-800 w-10 h-10 rounded-full opacity-0 md:opacity-100'
            onClick={() => setCollapsed(!collapsed)}
          >
            <Icon className='w-5 h-5' />
          </button>
        </div>
        <nav className='flex-grow'>
          <ul
            className={classNames({
              'my-2 flex flex-col gap-2 items-stretch': true,
            })}
          >
            {navItems.map((item, index) => {
              return (
                <li
                  key={index}
                  className={classNames({
                    'text-indigo-100 hover:bg-indigo-900 flex': true, //colors
                    'transition-colors duration-300': true, //animation
                    'rounded-md p-2 mx-3 gap-4 ': !collapsed,
                    'rounded-full p-2 mx-3 w-10 h-10': collapsed,
                  })}
                >
                  <Link to={item.to} className='flex gap-2'>
                    {item.icon} <span>{!collapsed && item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
