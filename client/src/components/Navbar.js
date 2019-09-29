import React from 'react';
import PropTypes from 'prop-types';
import {
  Navbar,
  Nav,
  FormControl,
  Button,
  Form,
  Container
} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
import { BrowserRouter as Router, NavLink } from 'react-router-dom';

const CommonNavbar = props => {
  return (
    <div>
      <Router>
        <Container>
          <Navbar bg='light' variant='light'>
            <Navbar.Brand href='/home'>ourCommerce</Navbar.Brand>
            <Nav className='mr-auto'>
              <NavLink to='/products'>Products</NavLink>
              <NavLink to='/featured'>Featured Products</NavLink>
              <NavLink to='/cart'>
                <FontAwesomeIcon icon={faShoppingCart} />
              </NavLink>
            </Nav>
            <Form inline>
              <FormControl
                type='text'
                placeholder='Search'
                className='mr-sm-2'
              />
              <Button variant='outline-primary'>Search</Button>
            </Form>
          </Navbar>
        </Container>
      </Router>
    </div>
  );
};

CommonNavbar.propTypes = {};

export default CommonNavbar;
