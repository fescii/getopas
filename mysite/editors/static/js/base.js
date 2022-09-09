// All Sidebar Links
let sidebarLinks = document.querySelectorAll('.link')

//Adding an event when mouse enter the element
sidebarLinks.forEach(link =>{
    link.addEventListener('mouseenter', (event) =>{
        let span = link.querySelector('#select')
        //span.classList.add('specific-link')
        link.classList.add('active-link')
        link.appendChild(span)
    })
})
//Adding an event When mouse leaves the element
sidebarLinks.forEach(link =>{
    link.addEventListener('mouseleave', (event) =>{
        let span = link.querySelector('#select')
       // span.classList.remove('specific-link')
        link.classList.remove('active-link')
    })
})

// Dropdown
 dropdownBtn = document.querySelector('#dropdown-btn')
 dropdownModal = document.querySelector('#profile-dropdown')

 dropdownBtn.addEventListener('click', (e) =>{
    if (dropdownModal.style.display === 'none'){
        dropdownModal.style.setProperty('display', 'block')
    }
    else{
        dropdownModal.style.setProperty('display', 'none')
    }
 })

// Closing Error and Success Messages
let closeBtns = document.querySelectorAll('.close')

closeBtns.forEach((btn)=>{
    btn.addEventListener('click',()=> {
        btn.parentElement.remove()
    })
})