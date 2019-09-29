import React from 'react';
import Home from '../components/Home';
import Products from '../components/Products';
import Featured from '../components/Featured';
import Cart from '../components/Cart';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CommonNavbar from '../components/Navbar';

export default function Routes() {
  return (
    <Router>
      <CommonNavbar />
      <Switch>
        <Route exact path='/' component={Home} />
        <Route path='/home' component={Home} />
        <Route path='/products' component={Products} />
        <Route path='/featured' component={Featured} />
        <Route path='/cart' component={Cart} />
      </Switch>
    </Router>
  );
}
