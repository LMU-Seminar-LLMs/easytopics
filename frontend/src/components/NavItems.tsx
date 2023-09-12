import React from 'react';
import {
  HomeIcon,
  ArrowUpTrayIcon,
  QuestionMarkCircleIcon,
  CubeTransparentIcon,
  ChartPieIcon,
  ArrowDownTrayIcon,
} from '@heroicons/react/24/outline';

/* CURRENTLY NOT USED */

export type NavItem = {
  label: string;
  to: string;
  icon: React.ReactNode;
};

export const NavItems: NavItem[] = [
  {
    label: 'Home',
    to: '/',
    icon: <HomeIcon className='w-6 h-6' />,
  },
  {
    label: 'Data',
    to: '/data',
    icon: <ArrowUpTrayIcon className='w-6 h-6' />,
  },
  {
    label: 'Q&A',
    to: '/qa',
    icon: <QuestionMarkCircleIcon className='w-6 h-6' />,
  },
  {
    label: 'Analysis',
    to: '/analysis',
    icon: <CubeTransparentIcon className='w-6 h-6' />,
  },
  {
    label: 'Results',
    to: '/results',
    icon: <ChartPieIcon className='w-6 h-6' />,
  },
  /*{
    label: 'Save',
    to: '/save',
    icon: <ArrowDownTrayIcon className='w-6 h-6' />,
  },*/
];
