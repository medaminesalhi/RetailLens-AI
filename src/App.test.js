import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders RetailLens and the upload options', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByText('RetailLens AI')).toBeInTheDocument();
  expect(screen.getByText(/Choisissez une méthode/)).toBeInTheDocument();
});
