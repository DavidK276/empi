import * as env from '$env/static/public';

export const INT_API_ENDPOINT = (env.EMPI_INT_API_ENDPOINT || 'http://127.0.0.1:8000/api').replace(/\/$/, '') + '/';
export const EXT_API_ENDPOINT = (env.EMPI_EXT_API_ENDPOINT || 'http://127.0.0.1:8000/api').replace(/\/$/, '') + '/';
export const TOKEN_COOKIE = 'sessiontoken';
export const SUPPORTED_LANGS = ['en', 'sk'];
export const ALLOW_TEXTENTRY_ATTR = false;
export const ENABLE_ATTRS = false;
export const PAGE_SIZE = 10;
export const TOKEN_REGEX = /[2346789BCDFGHJKMPQRTVWXY]{4}-[2346789BCDFGHJKMPQRTVWXY]{4}/g;