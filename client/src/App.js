import React, { Component } from 'react';
import HeaderContainer from './components/HeaderContainer';
import { Container, Row, Col } from 'reactstrap';

class App extends Component {
    render() {
        return (
        	<Container>
				<Row>
					<Col sm="12">
            			<HeaderContainer />
					</Col>
				</Row>
			</Container>
        );
    }
}

export default App;