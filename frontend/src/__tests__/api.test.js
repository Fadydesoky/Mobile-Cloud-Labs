import axios from 'axios';

// API call function
export const fetchData = async (url) => {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        throw new Error('Error fetching data');
    }
};

// API call with retry logic
export const fetchDataWithRetry = async (url, retries = 3) => {
    for (let i = 0; i < retries; i++) {
        try {
            const data = await fetchData(url);
            return data;
        } catch (error) {
            if (i === retries - 1) throw error; // if it's the last retry, throw error
        }
    }
};

// Jest tests for API calls
import { fetchData, fetchDataWithRetry } from './api';
import axios from 'axios';

jest.mock('axios');

describe('API Calls', () => {
    test('fetchData success', async () => {
        const data = { data: 'sample data' };
        axios.get.mockResolvedValue(data);

        const result = await fetchData('https://api.example.com/data');
        expect(result).toEqual(data);
    });

    test('fetchData failure', async () => {
        axios.get.mockRejectedValue(new Error('Error fetching data'));

        await expect(fetchData('https://api.example.com/data')).rejects.toThrow('Error fetching data');
    });

    test('fetchDataWithRetry success on first attempt', async () => {
        const data = { data: 'sample data' };
        axios.get.mockResolvedValue(data);

        const result = await fetchDataWithRetry('https://api.example.com/data');
        expect(result).toEqual(data);
    });

    test('fetchDataWithRetry retries on failure', async () => {
        const data = { data: 'sample data' };
        axios.get.mockRejectedValueOnce(new Error('Error fetching data'));
        axios.get.mockResolvedValueOnce(data);

        const result = await fetchDataWithRetry('https://api.example.com/data');
        expect(result).toEqual(data);
    });

    test('fetchDataWithRetry fails after all retries', async () => {
        axios.get.mockRejectedValue(new Error('Error fetching data'));

        await expect(fetchDataWithRetry('https://api.example.com/data')).rejects.toThrow('Error fetching data');
    });
});
