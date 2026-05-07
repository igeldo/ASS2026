package de.conciso.starter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class AuthorizationTokenFilter implements Filter {

    private final AuthorizationTokenHolder tokenHolder;

    public AuthorizationTokenFilter(AuthorizationTokenHolder tokenHolder) {
        this.tokenHolder = tokenHolder;
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        tokenHolder.setToken(((HttpServletRequest) servletRequest).getHeader("Authorization"));
        filterChain.doFilter(servletRequest, servletResponse);
    }
}
