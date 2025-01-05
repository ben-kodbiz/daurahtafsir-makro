function toggleTheme() {
    console.log("toggleTheme function called");
    const htmlElement = document.documentElement;
     if (htmlElement.classList.contains('light-theme')) {
        htmlElement.classList.remove('light-theme');
        htmlElement.classList.add('dark-theme');
         console.log("Dark theme activated");
    } else if (htmlElement.classList.contains('dark-theme')) {
         htmlElement.classList.remove('dark-theme');
          htmlElement.classList.add('sepia-theme');
        console.log("Sepia theme activated");
    } else if (htmlElement.classList.contains('sepia-theme')){
        htmlElement.classList.remove('sepia-theme');
        htmlElement.classList.add('light-theme');
          console.log("Light theme activated");
    }
    else {
          htmlElement.classList.add('light-theme');
          console.log("Light theme activated");
    }
}