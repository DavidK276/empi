import * as process from 'node:process';

let env;
if (typeof process != 'undefined') {
	env = process.env;
}

export const INT_API_ENDPOINT = (env?.INT_API_ENDPOINT || 'http://127.0.0.1:8000/api').replace(/\/$/, '')
export const EXT_API_ENDPOINT = (env?.EXT_API_ENDPOINT || 'http://127.0.0.1:8000/api').replace(/\/$/, '')
export const TOKEN_COOKIE = 'sessiontoken';
export const SUPPORTED_LANGS = ['en', 'sk'];
export const ALLOW_TEXTENTRY_ATTR = false;
export const PAGE_SIZE = 10;