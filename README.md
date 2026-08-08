# ASCII-Wires
<!DOCTYPE html>
<html lang="en">
<head>
<style>
  .typewriter {
    font-family: monospace;
    overflow: hidden; /* Ensures content is hidden until animation reveals it */
    border-right: 3px solid orange; /* The typing cursor */
    white-space: nowrap; /* Keeps the text on a single line */
    margin: 0 auto; 
    letter-spacing: 0.15em; 
    width: 0; /* Starts hidden */
    animation: 
      typing 3.5s steps(30, end) forwards,
      blink-caret 0.75s step-end infinite;
  }

  /* The typing animation */
  @keyframes typing {
    from { width: 0 }
    to { width: 100% }
  }

  /* The blinking cursor animation */
  @keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: orange; }
  }
</style>
</head>
<body>

  <h1 class="typewriter">Hello World, this is a typing effect.</h1>

</body>
</html>
