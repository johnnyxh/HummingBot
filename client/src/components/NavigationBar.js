import React, { Component } from 'react';
import { Nav } from 'reactstrap';
import NavigationItemContainer from './NavigationItemContainer';
import { NAV_ICON_MAP } from '../constants';

export default class NavigationBar extends Component {
	render() {
		return (
			<Nav justified tabs>
				{
					Object.entries(NAV_ICON_MAP).map(item => {
						return <NavigationItemContainer navigation={item[0]} icon={item[1]} />
					})
				}
			</Nav>
		);
	}
}