function setCookie(cname: string, cvalue: string, exdays: number, deleteFirst?: boolean) {
    if (deleteFirst !== undefined && deleteFirst) {
        document.cookie = `${cname}=; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
    }
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = `${cname}=${cvalue}; ${expires};`;
}

export {
    setCookie,
}