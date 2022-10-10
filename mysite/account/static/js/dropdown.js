/* Humbugger Menu */
const hamburgerMenu = document.querySelector('.hamburger'); //Selects the element with the class name of hamburger.
const menu = document.querySelector('.dashboard-sidebar');
if (hamburgerMenu != null) {
    //Creating an arrow function for changing the class to active.
    const menuIsActive = () => {
        //Selecting the hamburger menu and adding and removing the class of active on click.
        hamburgerMenu.classList.toggle('active');
        if (menu.style.display == 'block') {
            menu.style.setProperty('display', 'none');
        }
        else {
            menu.style.setProperty('display', 'block');
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
        if (footerModal.style.display === 'block') {
            footerModal.style.setProperty('display', 'none')
        }
        else {
            footerModal.style.setProperty('display', 'block')
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

