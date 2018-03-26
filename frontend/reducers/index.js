import {combineReducers} from "redux";
import {filter} from "./filter";
import {analysis} from "./analysis";

const rootReducer = combineReducers({
    filter,
    analysis
});

export default rootReducer;
