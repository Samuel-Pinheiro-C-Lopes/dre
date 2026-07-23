import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App Component', () => {
  it('renders the main heading', () => {
    render(<App />);
    const heading = screen.getByText(/Rule Extractor/i);
    expect(heading).toBeInTheDocument();
  });
  
  it('renders the upload zone', () => {
    render(<App />);
    const dropzoneText = screen.getByText(/Upload Document/i);
    expect(dropzoneText).toBeInTheDocument();
  });
});
