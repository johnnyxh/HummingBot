import React, { Component } from 'react';
import { NavItem, NavLink } from 'reactstrap';
import FontAwesome from 'react-fontawesome';

export default class NavigationItem extends Component {
	constructor() {
		super()
		this.onClickHandler = this.onClickHandler.bind(this);
	}

	onClickHandler() {
		this.props.changeNav(this.props.navigation)
	}

	render() {
		return (
			<NavItem>
				<NavLink href='#' active={this.props.currentView === this.props.navigation} onClick={this.onClickHandler}>
					<span className='fa-stack fa-2x'>
						<FontAwesome className='text-black' name='circle' stack='2x' style={{ textShadow: '0 1px 0 rgba(0, 0, 0, 0.1)' }} />
						<FontAwesome className='white' name={this.props.icon} stack='1x' inverse style={{ textShadow: '0 1px 0 rgba(0, 0, 0, 0.1)' }} />
					</span>
				</NavLink>
			</NavItem>
		);
	}
};