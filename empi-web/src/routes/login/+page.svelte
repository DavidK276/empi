<script lang="ts">
    import {API_ENDPOINT} from "$lib/constants";
    import {setCookie} from "$lib/functions";

    async function login(e: SubmitEvent) {
        let form = e.target as HTMLFormElement | undefined;
        let formData = new FormData(form, e.submitter)
        let response = await fetch(API_ENDPOINT + "rest-auth/login/", {
            body: formData,
            method: 'POST'
        });
        let responseJSON = await response.json();
        if (response.ok) {
            let key: string = responseJSON.key;
            setCookie("sessionid", key, 7, true);
        }
        else {
            let errors: Iterable<string> = responseJSON.non_field_errors;
            console.log(responseJSON);
            for (const error of errors) {
                let section: Element | null = document.querySelector(".login .error");
                if (section !== null) {
                    section.innerHTML += `<p style="color: red">${error}</p>`
                }
            }
        }
    }
</script>
<form on:submit|preventDefault={login} class="login">
    <section class="error"></section>
    <label for="username">Username: </label>
    <input type="text" id="username" name="username" required>
    <label for="password">Password: </label>
    <input type="text" id="password" name="password" required>
    <button type="submit" name="submit">Log in</button>
</form>
