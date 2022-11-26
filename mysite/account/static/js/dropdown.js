/* Humbugger Menu */
const hamburgerMenu = document.querySelector('.hamburger'); //Selects the element with the class name of hamburger.
const menu = document.querySelector('.dashboard-sidebar');
if (hamburgerMenu != null) {
    //Creating an arrow function for changing the class to active.
    const menuIsActive = () => {
        //Selecting the hamburger menu and adding and removing the class of active on click.
        try {
            footerBtn.style.setProperty('color', '#808080');
            footerModal.style.setProperty('display', 'none');
        }
        finally {
            hamburgerMenu.classList.toggle('active');
            if (menu.style.display == 'block') {
                menu.style.setProperty('display', 'none');
            }
            else {
                menu.style.setProperty('display', 'block');
            }
        }
    };
    //Adds an event listener of 'click' to the hamburger menu. Then we pass in the function we created where the class is toggled on and off.
    hamburgerMenu.addEventListener('click', menuIsActive);

}


// Dropdown
dropdownBtn = document.querySelector('#dropdown-btn')
dropdownModal = document.querySelector('#profile-dropdown')
if (dropdownBtn != null && dropdownModal != null) {
    dropdownBtn.addEventListener('click', (e) => {
        if (dropdownModal.style.display === 'block') {
            dropdownModal.style.setProperty('display', 'none')
        }
        else {
            dropdownModal.style.setProperty('display', 'block')
        }
    })
}

footerBtn = document.querySelector('#footer-btn')
footerModal = document.querySelector('#profile-footer')
if (footerBtn != null && footerModal != null) {
    footerBtn.addEventListener('click', (e) => {
        footerTxt = footerBtn.querySelector('.link-text')
        if (footerModal.style.display === 'block') {
            footerModal.style.setProperty('display', 'none')
            e.target.style.setProperty('color', '#808080')
            footerTxt.style.setProperty('color', '#808080')
        }
        else {
            try {
                if (menu.style.display == 'block') {
                    hamburgerMenu.classList.toggle('active');
                    menu.style.setProperty('display', 'none');
                }
            }
            finally {
                footerModal.style.setProperty('display', 'block')
                e.target.style.setProperty('color', 'rgb(255, 136, 0)')
                footerTxt.style.setProperty('color', 'rgb(255, 136, 0)')
            }
        }
    })
}



/* Feeds Dropdown */
moreButtons = document.querySelectorAll('#moreBtn')

if (moreButtons != null) {
    moreButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            parent = btn.parentElement;
            actionsModal = parent.lastElementChild;
            if (actionsModal.style.display == 'none') {
                actionsModal.style.setProperty("display", 'flex');
            }
            else {
                actionsModal.style.setProperty("display", 'none');
            }
        })
    });
}

// All Sidebar Links
let sidebarLinks = document.querySelectorAll('.link')
if (sidebarLinks != null) {
    //Adding an event when mouse enter the element
    sidebarLinks.forEach(link => {
        link.addEventListener('mouseenter', (event) => {
            let span = link.querySelector('#select')
            //span.classList.add('specific-link')
            link.classList.add('active-link')
        })
    })
    //Adding an event When mouse leaves the element
    sidebarLinks.forEach(link => {
        link.addEventListener('mouseleave', (event) => {
            let span = link.querySelector('#select')
            // span.classList.remove('specific-link')
            link.classList.remove('active-link')
        })
    })
}
// Closing Error and Success Messages
let closeButtons = document.querySelectorAll('.close')
if (closeButtons != null) {
    closeButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            btn.parentElement.remove()
        })
    })
}

// Close the dropdown if the user clicks outside of it
/*window.onclick = function (event) {
    if (!event.target.matches('#dropdown-btn')) {
        dropdownModal.style.setProperty("display", 'none');
    }
}*/


let data = {
    "alt": "#08b86f",
    "nav": "rgba(218, 215, 215, 0.087)",
    "body": "#000",
    "gray": "#a6a6a6",
    "link": "#007bff",
    "hover": "#1dbd7b",
    "accent": "#08b86f",
    "border": "1px solid #a2a3a342",
    "shadow": "0 12px 48px rgba(109, 117, 141, 0.2)",
    "unread": "rgba(90, 91, 91, 0.64)",
    "article": "#f2f2f2",
    "section": "#f2f2f2",
    "sidebar": "#a6a6a6",
    "summery": "#e5e5e5",
    "background": "#1a1a1a"
}