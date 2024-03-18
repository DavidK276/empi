<script lang="ts">
    // import { API_ENDPOINT } from "$lib/constants";
    import type { ActionData } from './$types';

    export let form: ActionData;

    // async function handleLoginResponse(response: Response) {
    //     let section: Element | null = document.querySelector(".login .error");
    //     let responseJSON = await response.json();
    //     if (response.ok) {
    //         const cookies = response.headers.getSetCookie();
    //         for (const cookie of cookies) {
    //             document.cookie = cookie;
    //         }
    //         if (section !== null) {
    //             section.innerHTML += '<p style="color: green">Prihlásenie úspešné</p>';
    //         }
    //     }
    //     else {
    //         let errors: Iterable<string> = responseJSON.non_field_errors;
    //         console.log(responseJSON);
    //         for (const error of errors) {
    //             if (section !== null) {
    //                 section.innerHTML += `<p style="color: red">${error}</p>`;
    //             }
    //         }
    //     }
    // }

    // async function login(event: { currentTarget: EventTarget & HTMLFormElement }) {
    //     let formData = new FormData(event.currentTarget);
    //     let maybeEmail = formData.get("username")?.toString();
    //     if (maybeEmail?.includes('@')) {
    //         formData.delete("username");
    //         formData.append("email", maybeEmail);
    //     }
    //     let response = await fetch(API_ENDPOINT + "rest-auth/login/", {
    //         body: formData,
    //         method: 'POST'
    //     });
    //     await handleLoginResponse(response);
    // }
</script>
{#if form?.success === true}
    <p>Prihlásenie bolo úspešné!</p>
{:else if form?.success === false}
    <p>Nepodarilo sa prihlásiť</p>
{/if}
<form method="POST">
    <section class="error"></section>
    <label for="username">Username: </label>
    <input type="text" id="username" name="username" required>
    <label for="password">Password: </label>
    <input type="password" id="password" name="password" required>
    <button type="submit" name="submit">Log in</button>
</form>
