import { addFormErrors } from "$lib/functions";
import FormResultMessage from "$lib/components/FormResultMessage.svelte";
import { mount } from "svelte";

// @ts-expect-error this is JS, no idea why TS is even screaming here
export async function universalEnhance({formElement, submitter}, {idleMessage, runningMessage, reset, invalidateAll, printSuccessMessage = true}) {
	if (submitter != null) {
		submitter.toggleAttribute('disabled');
		submitter.innerHTML = runningMessage;
	}
	// @ts-expect-error this is JS, no idea why TS is even screaming here
	return async ({update, result}) => {
		await update({invalidateAll, reset});
		const submitDiv = formElement.children.namedItem('submit-div');
		if (printSuccessMessage && submitDiv != null) {
			mount(FormResultMessage, {target: submitDiv, props: {result}});
		}
		if (result.type === 'failure') {
			addFormErrors(result.data?.errors, formElement);
		}
		submitter.toggleAttribute('disabled');
		submitter.innerHTML = idleMessage;
	};
}