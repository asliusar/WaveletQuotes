import React from 'react';
import autobind from 'autobind-decorator';
import {connect} from 'react-redux';

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
};


class Footer extends React.Component {

    render() {
        return (
            <div className={styles.container}>

            </div>
        );
    }
}

Footer.propTypes = propTypes;

function mapStateToProps(state) {
    return state;
}

export default connect(mapStateToProps)(Footer);