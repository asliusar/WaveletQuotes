export class ShowList {
    constructor(initialState) {
        this.isLoading = false;
        this.list = [];
        this.page = 1;
        Object.assign(this, initialState);
    }
}