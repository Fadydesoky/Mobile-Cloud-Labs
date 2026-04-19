import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import App, { fetchData, fetchDataWithRetry } from './App';

// Mock fetch globally
beforeAll(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.clearAllMocks();
});

describe('App Component', () => {
  beforeEach(() => {
    // Default mock for health checks
    fetch.mockImplementation((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({ 
          ok: true, 
          json: () => Promise.resolve({ status: 'healthy' }) 
        });
      }
      return Promise.resolve({ 
        ok: true, 
        json: () => Promise.resolve({}) 
      });
    });
  });

  test('renders Mobile Cloud System header', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Mobile Cloud System/i)).toBeInTheDocument();
  });

  test('renders Run Simulation button', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Run Simulation/i)).toBeInTheDocument();
  });

  test('renders Observability Dashboard title', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Observability Dashboard/i)).toBeInTheDocument();
  });

  test('toggles dark/light mode', async () => {
    await act(async () => {
      render(<App />);
    });
    const toggleButton = screen.getByText(/Light/i);
    
    await act(async () => {
      fireEvent.click(toggleButton);
    });
    
    expect(screen.getByText(/Dark/i)).toBeInTheDocument();
  });

  test('renders System Architecture section', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/System Architecture/i)).toBeInTheDocument();
  });

  test('renders service status cards', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Order Service/i)).toBeInTheDocument();
    expect(screen.getByText(/Product Service/i)).toBeInTheDocument();
  });

  test('shows Processing when simulation runs', async () => {
    fetch.mockImplementation((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({ ok: true });
      }
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            ok: true,
            json: () => Promise.resolve({
              order_id: 'ORD-123',
              product: 'Test Product',
              quantity: 2,
              total_price: 100
            })
          });
        }, 100);
      });
    });

    await act(async () => {
      render(<App />);
    });
    
    const button = screen.getByText(/Run Simulation/i);
    
    await act(async () => {
      fireEvent.click(button);
    });
    
    expect(screen.getByText(/Processing.../i)).toBeInTheDocument();
  });

  test('displays error state on fetch failure', async () => {
    fetch.mockImplementation((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({ ok: true });
      }
      return Promise.reject(new Error('Network error'));
    });

    await act(async () => {
      render(<App />);
    });
    
    const button = screen.getByText(/Run Simulation/i);
    
    await act(async () => {
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(screen.getByText(/Error/i)).toBeInTheDocument();
    });
  });

  test('displays metrics cards', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Total Requests/i)).toBeInTheDocument();
    expect(screen.getByText(/Avg Latency/i)).toBeInTheDocument();
  });

  test('displays API Response section', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/API Response/i)).toBeInTheDocument();
  });

  test('displays System Logs section', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/System Logs/i)).toBeInTheDocument();
  });

  test('renders navigation tabs', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/overview/i)).toBeInTheDocument();
    expect(screen.getByText(/services/i)).toBeInTheDocument();
    expect(screen.getByText(/logs/i)).toBeInTheDocument();
  });
});

describe('API Functions', () => {
  test('fetchDataWithRetry is a function', () => {
    expect(typeof fetchDataWithRetry).toBe('function');
  });

  test('fetchData is exported and is a function', () => {
    expect(typeof fetchData).toBe('function');
  });
});

describe('App Footer', () => {
  beforeEach(() => {
    fetch.mockImplementation(() => Promise.resolve({ ok: true }));
  });

  test('renders footer with technology stack', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText(/Docker \+ Kubernetes \+ Redis/i)).toBeInTheDocument();
  });
});
