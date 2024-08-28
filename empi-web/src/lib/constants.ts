import * as process from 'node:process';

let env;
if (typeof process != 'undefined') {
	env = process.env;
}

const API_PREFIX = (env?.API_PREFIX || 'http://127.0.0.1:8000/').replace(/\/$/, '') + '/';
export const INT_SERVER_URL = (env?.INT_SERVER_URL || 'http://127.0.0.1:8000/').replace(/\/$/, '') + '/';
export const EXT_SERVER_URL = (env?.EXT_SERVER_URL || 'http://127.0.0.1:8000/').replace(/\/$/, '') + '/';
export const INT_API_ENDPOINT = INT_SERVER_URL + API_PREFIX;
export const EXT_API_ENDPOINT = EXT_SERVER_URL + API_PREFIX;
export const TOKEN_COOKIE = 'sessiontoken';
export const SUPPORTED_LANGS = ['en', 'sk'];
export const ALLOW_TEXTENTRY_ATTR = false;
export const PAGE_SIZE = 10;