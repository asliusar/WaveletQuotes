import React from 'react';
import {connect} from 'react-redux';
import styles from './css/styles.css'

import Header from '../../components/header/Header';
import Footer from '../../components/Footer';

const propTypes = {
    children: React.PropTypes.object,
};

class App extends React.Component {

    render() {
        return (
            <div className={styles.container}>
                <Header {...this.props} />
                <div className={styles.content}>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

App.propTypes = propTypes;


function mapStateToProps(state) {
    return state;
}

export default connect(mapStateToProps)(App);
