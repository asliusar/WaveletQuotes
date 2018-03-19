import React from 'react';
import autobind from 'autobind-decorator';
import {connect} from 'react-redux';
import {IconMenu, IconButton, MenuItem, AppBar, FlatButton, Drawer, Divider} from 'material-ui';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import FriendsIcon from 'material-ui/svg-icons/action/face';
import ShowsIcon from 'material-ui/svg-icons/notification/live-tv';
import CalendarIcon from 'material-ui/svg-icons/action/date-range';
import {browserHistory} from 'react-router';


import styles from './css/styles.css';
import {toggleDrawer} from '../../actions/header/drawer';
import {closeDrawer} from '../../actions/header/drawer';

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    user: React.PropTypes.object,
    drawer: React.PropTypes.object
};

class Header extends React.Component {

    static handleMenuItemClickedEvent() {
        browserHistory.push('/');
    };

    static handleMenuShowsClickedEvent() {
        browserHistory.push('/');
    };

    static handleMenuCalendarClickedEvent() {
        browserHistory.push('/');
    };

    static handleMenuFriendsClickedEvent() {
        browserHistory.push('/friends');
    };

    static handleClickLoginClientEvent() {
        browserHistory.push('/login');
    };

    @autobind
    handleCloseDrawer() {
        const {dispatch} = this.props;
        dispatch(closeDrawer());
    };

    @autobind
    handleLogoutClickEvent() {
        const {dispatch} = this.props;
        dispatch(logoutUser());
    };

    render() {
        return (
            <div className={styles.container}>
                <AppBar
                    className={styles.header_content}
                    title="TV Shows"
                    onTitleTouchTap={Header.handleMenuItemClickedEvent}
                    onLeftIconButtonTouchTap={this.handleToggleDrawer}
                />
            </div>
        );
    }
}

Header.propTypes = propTypes;

function mapStateToProps(state) {
    const {user, drawer} = state;
    return {
        user,
        drawer
    };
}

export default connect(mapStateToProps)(Header);