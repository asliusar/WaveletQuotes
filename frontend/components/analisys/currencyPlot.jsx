import React from "react";
import {connect} from "react-redux";
import styles from "./css/styles.css";

export const CurrencyPlot = (image) => (
    <div className={styles.container}>
        <image src={image}/>
    </div>
);