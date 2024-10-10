import { addFormErrors } from "$lib/functions";
import FormResultMessage from "$lib/components/FormResultMessage.svelte";

export async function universalEnhance({formElement, submitter}, {idleMessage, runningMessage, reset, invalidateAll}) {
	if (submitter != null) {
		submitter.toggleAttribute('disabled');
		submitter.innerHTML = runningMessage;
	}
	return async ({update, result}) => {
		await update({invalidateAll, reset});
		const submitDiv = formElement.children.namedItem('submit-div');
		if (submitDiv != null) {
			new FormResultMessage({target: submitDiv, props: {result}});
		}
		if (result.type === 'failure') {
			addFormErrors(result.data?.errors, formElement);
		}
		submitter.toggleAttribute('disabled');
		submitter.innerHTML = idleMessage;
	};
}