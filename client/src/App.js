import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';

import UserHeaderContainer from './components/UserHeaderContainer';
import HeaderContainer from './components/HeaderContainer';
import NavigationBar from './components/NavigationBar';
import ContentContainer from './components/ContentContainer';

class App extends Component {
    render() {
        return (
        	<Container>
				<Row>
					<Col sm="12">
                        <UserHeaderContainer />
            			<HeaderContainer />
            			<NavigationBar />
                        <ContentContainer />
					</Col>
				</Row>
			</Container>
        );
    }
}

export default App;