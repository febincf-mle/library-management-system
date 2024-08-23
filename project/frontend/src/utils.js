const handlePost = async (urlRoute, body, headers={}) => {

    const response = await fetch(`http://127.0.0.1:5000/api/${urlRoute}`, {
        method:'POST',
        headers: {
            ...headers,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
    });
    
    const data = await response.json();

    return data;
};


export default handlePost;