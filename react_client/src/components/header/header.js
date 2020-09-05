import React from 'react';
// import logo from './logo.svg';
import './Header.css';

import CountUp from 'react-countup';
import Headroom from 'react-headroom'
function Header() {
  return (
    <Headroom><CountUp start={0} end={160526} /></Headroom>
    );
}

export default Header;
