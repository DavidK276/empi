export const addFormError = (element: HTMLElement, text: string) => {
	const errorElement = document.getElementById(`${element.id}_error`);
	if (errorElement == null) {
		const error = `<p class="error-msg auto-error" id="${element.id}_error">${text}</p>`;
		element.insertAdjacentHTML('afterend', error);
		element.classList.add('error');
	}
	else {
		errorElement.innerText = text;
	}
};

export const addFormErrors = (formErrors: { [x: string]: string[]; }, formElement: HTMLFormElement) => {
	Object.keys(formErrors).forEach(key => {
		const element = formElement.elements.namedItem(key) as HTMLElement | null;
		if (element != null) {
			const errors = formErrors[key] as string[];
			errors.forEach(error => {
				addFormError(element, error);
			});
		}
	});
};

export const removeFormError = (element: HTMLElement) => {
	element.classList.remove('error');
	const errorElement = document.getElementById(`${element.id}_error`);
	errorElement?.remove();
};

export const convertFormData = (args: { formData: FormData, stringify?: boolean }) => {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const object: any = {};
	args.formData.forEach((formDataEntryValue, key) => {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		let value: any = formDataEntryValue;
		if (value === '__NULL__') {
			value = null;
		}
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

export function columnify<Type>(items: Type[], columnSize: number) {
	const result: Type[][] = [];
	let column: Type[] = [];
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

export function paginationParams(urlSearchParams: URLSearchParams) {
	const result = new URLSearchParams();
	if (urlSearchParams.has('limit')) {
		result.set('limit', urlSearchParams.get('limit')!);
	}
	if (urlSearchParams.has('offset')) {
		result.set('offset', urlSearchParams.get('offset')!);
	}
	return result;
}

export function getCurrentAcadYear() {
	const currentYear = new Date().getFullYear();
	const currentMonth = new Date().getMonth();
	const startYear = (currentMonth >= 8) ? currentYear : currentYear - 1;

	return `${startYear}/${(startYear + 1) % 100}`;
}

export function localeDateStringFromUTCString(utcString: string) {
	return new Date(utcString)
			.toLocaleString(undefined, {
				weekday: "long",
				day: "numeric",
				month: "long",
				year: "numeric",
				hour: "numeric",
				minute: "numeric"
			});
}

export function textAreaAdjustSize(event: Event) {
	const element = event.target as HTMLTextAreaElement;
	element.rows = (element.value.match(/\n/g) || []).length + 1;
}