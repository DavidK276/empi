import { col, error as e } from '$lib/style.css';

export function setCookie(cname: string, cvalue: string, exdays: number, deleteFirst?: boolean) {
	if (deleteFirst !== undefined && deleteFirst) {
		document.cookie = `${cname}=; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
	}
	const d = new Date();
	d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
	const expires = 'expires=' + d.toUTCString();
	document.cookie = `${cname}=${cvalue}; ${expires};`;
}

export function parseCookie(cookieString: string): {
	name: string,
	value: string,
	opts: Record<string, string> & { path: string }
} {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const result: any = {
		name: '',
		value: '',
		opts: {
			path: '/',
			partitioned: false,
			httpOnly: false,
			secure: false
		}
	};
	const nameValueStrings = cookieString.split(';');
	const nameValuePairs: string[][] = [];
	for (let i = 0; i < nameValueStrings.length; i++) {
		const [name, value] = nameValueStrings[i].trim().split('=', 2);
		nameValuePairs[i] = [name.toLowerCase(), value];
	}
	for (const nameValue of nameValuePairs) {
		const [name, value] = nameValue;
		if (name === 'domain') {
			result.opts.domain = value;
		}
		else if (name === 'expires') {
			result.opts.expires = new Date(Date.parse(value));
		}
		else if (name === 'max-age') {
			result.opts.maxAge = Number.parseInt(value);
		}
		else if (name === 'partitioned') {
			result.opts.partitioned = true;
		}
		else if (name === 'path') {
			result.opts.path = value;
		}
		else if (name === 'samesite') {
			result.opts.sameSite = value.toLowerCase();
		}
		else if (name === 'secure') {
			result.opts.secure = true;
		}
		else if (name === 'httponly') {
			result.opts.httpOnly = true;
		}
		else {
			result.name = name;
			result.value = value;
		}
	}
	return result;
}

export const toggleDropdown = (event: MouseEvent) => {
	const target = event.target as HTMLElement;
	target.parentElement?.classList.toggle('show');
};

export const addFormError = (element: HTMLElement, text: string) => {
	const errorElement = document.getElementById(`${element.id}_error`);
	if (errorElement == null) {
		const error = `<span class="${e}" id="${element.id}_error">${text}</span>`;
		element.insertAdjacentHTML('afterend', error);
		element.classList.add('error');
	}
	else {
		errorElement.innerText = text;
	}
};

export const removeFormError = (element: HTMLElement) => {
	element.classList.remove('error');
	const errorElement = document.getElementById(`${element.id}_error`);
	errorElement?.remove();
};

export const getUserIdFromUrl = (url: string) => {
	const match = url.match(/\/user\/([0-9]+)\/?/);
	if (match != null) {
		return parseInt(match[1]);
	}
	return null;
};

export const convertFormData = (args: { formData: FormData, stringify?: boolean }) => {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const object: any = {};
	args.formData.forEach((value, key) => {
		if (key.endsWith('[]')) {
			key = key.slice(0, -2);
			if (!Reflect.has(object, key)) {
				object[key] = [];
			}
			if (key !== '__blank__') {
				object[key].push(value);
			}
		}
		else {
			if (!Reflect.has(object, key)) {
				object[key] = value;
				return;
			}
			if (!Array.isArray(object[key])) {
				object[key] = [object[key]];
			}
			object[key].push(value);
		}
	});
	if (args.stringify === false) {
		return object;
	}
	return JSON.stringify(object);
};

export function columnify<Type>(items: Array<Type>, columnSize: number) {
	const result: Array<Array<Type>> = [];
	let column: Array<Type> = [];
	for (let i = 0; i < items.length; i++) {
		if (column.length == columnSize) {
			result.push(column);
			column = [];
		}
		column.push(items[i]);
	}
	if (column.length > 0) {
		result.push(column);
	}
	return result;
}