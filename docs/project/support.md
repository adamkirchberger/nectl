<!--
 Copyright (C) 2022 Adam Kirchberger

 This file is part of Nectl.

 Nectl is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Nectl is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Nectl.  If not, see <http://www.gnu.org/licenses/>.
-->

# Support & Help

This project is open source and completely free to use for personal and commercial projects under the terms of the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

If you encounter a problem or have a general question please raise an issue on Github.

Should you need additional help or are looking for automation consultancy please feel free to get in touch via our contact form.

---

## Contact Form

</br>
<!-- Contact form style -->
<head>
  <style>
    input[type="text"],
    select,
    textarea {
      font-family: inherit;
      width: 100%; /* Full width */
      padding: 12px; /* Some padding */
      border: 1px solid #ccc; /* Gray border */
      border-radius: 4px; /* Rounded borders */
      box-sizing: border-box; /* Make sure that padding and width stays in place  */
      margin-top: 6px; /* Add a top margin */
      margin-bottom: 16px; /* Bottom margin */
      resize: vertical; /* Allow the user to vertically resize the textarea (not  horizontally) */
    }
    /* Style the submit button with a specific background color etc */
    input[type="submit"] {
      background-color: var(--theme-color, #42b983);
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    /* When moving the mouse over the submit button, add a darker green color */
    input[type="submit"]:hover {
      color: inherit;
      opacity: 0.8;
    }
  </style>
</head>

<div class="form-container">
  <form
    name="contact"
    method="POST"
    data-netlify="true"
    data-netlify-recaptcha="true"
  >
    <label for="name">Name</label>
    <input type="text" id="name" name="name" placeholder="Your name..">
    <label for="email">Email</label>
    <input type="text" id="email" name="email" placeholder="Your email..">
    <label for="message">Message</label>
    <textarea id="message" name="message" placeholder="Your message.." style="height:200px"></textarea>
    <div data-netlify-recaptcha="true"></div>
    <input type="submit" value="Submit">
  </form>
</div>
