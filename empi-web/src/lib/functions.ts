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
		const error = `<span style="color: red; display: block; margin: 4px 0" id="${element.id}_error">${text}</span>`;
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
