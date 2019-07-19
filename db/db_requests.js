import axios from 'axios';

const getInventory = () => new Promise((resolve, reject) => {
    axios.get('http://127.0.0.1:5000/inventory')
    .then((result) => {
        document.write(result);
    })  
})

export default { getInventory };