import React from 'react';
import autobind from 'autobind-decorator'
import ShowListElement from './showPanel';
import styles from './css/styles.css'

const propTypes = {
    dispatch: React.PropTypes.func.isRequired,
    showList: React.PropTypes.object
};


class ShowList extends React.Component {
    render() {
        return (
            <div className={styles.container}>
                {
                    this.props.showList.list.map((showInfo) =>
                        <ShowListElement
                            dispatch={this.props.dispatch}
                            showInfo={showInfo}
                        />
                    )
                }
            </div>
        );
    }
}

ShowList.propTypes = propTypes;
export default ShowList;
