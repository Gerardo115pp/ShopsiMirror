let intersectionObserver;

function ensureIntersectionObserver() {
    if (intersectionObserver) {
        return;
    }

    intersectionObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            // entred the viewport
            if (entry.isIntersecting) {
                const event_name = entry.isIntersecting ? 'viewportEnter' : 'viewportLeave';
                const event = new CustomEvent(event_name);
                entry.target.dispatchEvent(event);
            }
        });
    })
}

const viewport = e => {
    ensureIntersectionObserver();
    intersectionObserver.observe(e);
    
    return {
        destroy: () => {
            intersectionObserver.unobserve(e);
        }
    };
}

export default viewport;