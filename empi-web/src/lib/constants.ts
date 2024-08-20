import * as process from 'node:process';

let env;
if (typeof process != 'undefined') {
	env = process.env;
}

export const INT_SERVER_URL = (env?.INT_SERVER_URL || 'http://127.0.0.1:8000/').replace(/\/$/, '') + '/';
export const EXT_SERVER_URL = 'http://127.0.0.1:8000/';
export const INT_API_ENDPOINT = INT_SERVER_URL + 'api/';
export const EXT_API_ENDPOINT = EXT_SERVER_URL + 'api/';
export const TOKEN_COOKIE = 'sessiontoken';
export const SUPPORTED_LANGS = ['en', 'sk'];
export const ALLOW_TEXTENTRY_ATTR = false;
export const PAGE_SIZE = 10;