import axios from 'axios';
import { fetchData, fetchDataWithRetry } from '../api';

jest.mock('axios');

describe('API Calls', () => {

  test('fetchData success', async () => {
    const mockResponse = { data: 'sample data' };
    axios.get.mockResolvedValue({ data: mockResponse });

    const result = await fetchData('https://api.example.com/data');
    expect(result).toEqual(mockResponse);
  });

  test('fetchData failure', async () => {
    axios.get.mockRejectedValue(new Error());

    await expect(
      fetchData('https://api.example.com/data')
    ).rejects.toThrow('Error fetching data');
  });

  test('fetchDataWithRetry success on retry', async () => {
    const mockResponse = { data: 'sample data' };

    axios.get
      .mockRejectedValueOnce(new Error())
      .mockResolvedValueOnce({ data: mockResponse });

    const result = await fetchDataWithRetry('https://api.example.com/data', 2);
    expect(result).toEqual(mockResponse);
  });

  test('fetchDataWithRetry fails after retries', async () => {
    axios.get.mockRejectedValue(new Error());

    await expect(
      fetchDataWithRetry('https://api.example.com/data', 2)
    ).rejects.toThrow('Error fetching data');
  });

});
