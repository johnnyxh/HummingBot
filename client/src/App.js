import React, { Component } from 'react';
import HeaderContainer from './components/HeaderContainer';
import NavigationBar from './components/NavigationBar';
import { Container, Row, Col } from 'reactstrap';

class App extends Component {
    render() {
        return (
        	<Container>
				<Row>
					<Col sm="12">
            			<HeaderContainer />
            			<NavigationBar />
					</Col>
				</Row>
			</Container>
        );
    }
}

export default App;