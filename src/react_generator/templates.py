"""Code templates stored as pure data.

Sentinel-based substitution (`__NAME__`, `__PASCAL__`, `__CAMEL__`) is used
instead of str.format, so the templates remain readable TSX/TS code without
doubled braces or conflicts with JavaScript template literals such as `${...}`.
"""



def render(template:str, *, name: str, pascal: str, camel: str) -> str:
    """Replace the sentinels.
        The three markers do not overlap, so the replacement order does not matter.
    """
    return (
        template
        .replace("__NAME__", name)
        .replace("__PASCAL__", pascal)
        .replace("__CAMEL__", camel)
    )

# --- component -------------------------------------------------------------

COMPONENT_TSX = """import React from 'react';
import styles from './__NAME__.module.scss';
import { __NAME__Props } from './__NAME__.types';

const __NAME__: React.FC<__NAME__Props> = () => {
  return (
    <div className={styles.container}>
      <h1>__NAME__ Component</h1>
    </div>
  );
};

export default __NAME__;
"""

COMPONENT_SCSS = """.container {
  // Add your styles here
}
"""

COMPONENT_TEST = """import React from 'react';
import { render, screen } from '@testing-library/react';
import __NAME__ from './__NAME__';

describe('__NAME__', () => {
  it('renders without crashing', () => {
    render(<__NAME__ />);
    expect(screen.getByText('__NAME__ Component')).toBeInTheDocument();
  });
});
"""

COMPONENT_TYPES = """export interface __NAME__Props {
  // Define your props here
}
"""

# --- service ---------------------------------------------------------------

SERVICE_TS = """export class __NAME__ {
  private static instance: __NAME__;

  private constructor() {
    // Private constructor for singleton pattern
  }

  public static getInstance(): __NAME__ {
    if (!__NAME__.instance) {
      __NAME__.instance = new __NAME__();
    }
    return __NAME__.instance;
  }

  public async getData(): Promise<unknown> {
    // Implement your logic
    return {};
  }
}

export default __NAME__.getInstance();
"""

SERVICE_TEST = """import singleton from './__NAME__';

describe('__NAME__', () => {
  it('should be a singleton', () => {
    expect(singleton).toBe(singleton);
  });

  it('should expose getData', () => {
    expect(singleton.getData).toBeDefined();
  });
});
"""

SERVICE_FUNCTIONAL_TS = """export async function getData(): Promise<unknown> {
  // Implement your logic
  return {};
}
"""

# --- hook ------------------------------------------------------------------

HOOK_TS = """import { useState, useEffect } from 'react';

export const __NAME__ = () => {
  const [data, setData] = useState<unknown>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Add your hook logic here
  }, []);

  return { data, loading, error };
};

export default __NAME__;
"""

HOOK_TEST = """import { renderHook } from '@testing-library/react';
import { __NAME__ } from './__NAME__';

describe('__NAME__', () => {
  it('should return initial state', () => {
    const { result } = renderHook(() => __NAME__());

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });
});
"""

# --- redux -----------------------------------------------------------------

REDUX_TS = """import { createSlice, PayloadAction } from '@reduxjs/toolkit';
// import type { RootState } from '../store';

export interface __PASCAL__State {
  value: number;
  status: 'idle' | 'loading' | 'failed';
}

const initialState: __PASCAL__State = {
  value: 0,
  status: 'idle',
};

export const __NAME__ = createSlice({
  name: '__CAMEL__',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = __NAME__.actions;

// export const selectValue = (state: RootState) => state.__CAMEL__.value;

export default __NAME__.reducer;
"""

REDUX_TEST = """import reducer, { __PASCAL__State, increment, decrement } from './__NAME__';

describe('__NAME__ reducer', () => {
  const initialState: __PASCAL__State = {
    value: 3,
    status: 'idle',
  };

  it('should handle initial state', () => {
    expect(reducer(undefined, { type: 'unknown' })).toEqual({
      value: 0,
      status: 'idle',
    });
  });

  it('should handle increment', () => {
    expect(reducer(initialState, increment()).value).toEqual(4);
  });

  it('should handle decrement', () => {
    expect(reducer(initialState, decrement()).value).toEqual(2);
  });
});
"""

# --- context ---------------------------------------------------------------

CONTEXT_TSX = """import React, { createContext, useContext, useState, useMemo } from 'react';
import { __NAME__Props, __NAME__Type } from './__NAME__.types';

const __NAME__ = createContext<__NAME__Type | undefined>(undefined);

export const __PASCAL__Provider: React.FC<__NAME__Props> = ({ children }) => {
  const [value, setValue] = useState<string>('Default Value');

  const contextValue = useMemo(() => ({ value, setValue }), [value]);

  return (
    <__NAME__.Provider value={contextValue}>
      {children}
    </__NAME__.Provider>
  );
};

export const use__PASCAL__ = (): __NAME__Type => {
  const context = useContext(__NAME__);
  if (context === undefined) {
    throw new Error('use__PASCAL__ must be used within a __PASCAL__Provider');
  }
  return context;
};
"""

CONTEXT_TYPES = """import React from 'react';

export interface __NAME__Props {
  children: React.ReactNode;
}

export interface __NAME__Type {
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string>>;
}
"""

CONTEXT_TEST = """import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { __PASCAL__Provider, use__PASCAL__ } from './__NAME__';

const TestComponent: React.FC = () => {
  const { value, setValue } = use__PASCAL__();
  return (
    <div>
      <span>{value}</span>
      <button onClick={() => setValue('New Value')}>Change</button>
    </div>
  );
};

describe('__NAME__', () => {
  it('provides the default value and allows updates', async () => {
    render(
      <__PASCAL__Provider>
        <TestComponent />
      </__PASCAL__Provider>
    );

    expect(screen.getByText('Default Value')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: /change/i }));
    expect(screen.getByText('New Value')).toBeInTheDocument();
  });

  it('throws when used outside a provider', () => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => render(<TestComponent />)).toThrow(
      'use__PASCAL__ must be used within a __PASCAL__Provider'
    );
    jest.restoreAllMocks();
  });
});
"""